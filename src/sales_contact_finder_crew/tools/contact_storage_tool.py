import json
import os
from typing import Type, Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from crewai.tools import BaseTool

# Load environment variables from .env file
load_dotenv()


class ContactStorageInput(BaseModel):
    """Input schema for ContactStorageTool."""

    contact_info: str = Field(
        description="JSON string containing company name and contacts information. "
        "Format: {'company_name': 'Company Name', 'contacts': [{'name': 'Name', 'title': 'Title', 'linkedin_url': 'URL', 'phone': 'Phone', 'email': 'Email'}]}"
    )


class ContactStorageTool(BaseTool):
    """
    Tool for storing contact information in GibsonAI database via hosted API.

    This tool saves contact information for sales prospects, including company
    details and individual contact information with their roles and contact methods.
    """

    name: str = "ContactStorageTool"
    description: str = """
    Saves contact information in a GibsonAI database using the hosted API. 
    
    Expected payload format:
    {
        "company_name": "Company Name", 
        "contacts": [
            {
                "name": "Contact Name",
                "title": "Job Title", 
                "linkedin_url": "LinkedIn URL or N/A",
                "phone": "Phone number or N/A",
                "email": "Email address or N/A"
            }
        ]
    }
    
    If values for phone and email are not available, they should be set to "N/A".
    The tool will create the company record first, then add all contacts associated with that company.
    """
    args_schema: Type[BaseModel] = ContactStorageInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize API configuration
        self._api_base_url = "https://api.gibsonai.com/v1/-"
        self._api_key = os.getenv("GIBSONAI_API_KEY")

        if not self._api_key:
            raise ValueError(
                "Missing GIBSONAI_API_KEY environment variable. "
                "Please set this in your .env file or environment."
            )

    def _run(self, contact_info: str) -> str:
        """
        Execute the contact storage operation.

        Args:
            contact_info: JSON string containing company and contacts data

        Returns:
            String indicating success or failure of the operation
        """
        try:
            # Parse the contact info if it's a string
            if isinstance(contact_info, str):
                contact_data = json.loads(contact_info)
            else:
                contact_data = contact_info

            # Validate required fields
            if "company_name" not in contact_data:
                return "Error: Missing 'company_name' in contact data"

            if "contacts" not in contact_data or not contact_data["contacts"]:
                return "Error: Missing or empty 'contacts' array in contact data"

            company_name = contact_data["company_name"]
            contacts = contact_data["contacts"]

            # Step 1: Create/insert company record
            company_payload = {"name": company_name}

            try:
                response = requests.post(
                    f"{self._api_base_url}/sales-company",
                    json=company_payload,
                    headers={"X-Gibson-API-Key": self._api_key},
                    timeout=30,
                )
                response.raise_for_status()
                company_result = response.json()
                company_id = company_result.get("id")

                if not company_id:
                    return f"Error: Failed to get company ID from API response: {company_result}"

                print(
                    f"Successfully created/found company '{company_name}' with ID: {company_id}"
                )

            except requests.exceptions.RequestException as e:
                return f"Error creating company record: {str(e)}"

            # Step 2: Create contact records
            successful_contacts = []
            failed_contacts = []

            for contact in contacts:
                try:
                    # Validate required contact fields
                    required_fields = ["name", "title"]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in contact or not contact[field]
                    ]

                    if missing_fields:
                        failed_contacts.append(
                            f"{contact.get('name', 'Unknown')}: Missing {', '.join(missing_fields)}"
                        )
                        continue

                    contact_payload = {
                        "company_id": company_id,
                        "name": contact["name"],
                        "title": contact["title"],
                        "linkedin_url": contact.get("linkedin_url", "N/A"),
                        "phone": contact.get("phone", "N/A"),
                        "email": contact.get("email", "N/A"),
                    }

                    response = requests.post(
                        f"{self._api_base_url}/sales-contact",
                        json=contact_payload,
                        headers={"X-Gibson-API-Key": self._api_key},
                        timeout=30,
                    )
                    response.raise_for_status()

                    successful_contacts.append(contact["name"])
                    print(
                        f"Successfully stored contact: {contact['name']} ({contact['title']})"
                    )

                except requests.exceptions.RequestException as e:
                    failed_contacts.append(
                        f"{contact.get('name', 'Unknown')}: {str(e)}"
                    )
                    print(
                        f"Failed to store contact {contact.get('name', 'Unknown')}: {str(e)}"
                    )

            # Prepare result summary
            result_parts = []
            result_parts.append(f"Company '{company_name}' processed successfully.")

            if successful_contacts:
                result_parts.append(
                    f"Successfully stored {len(successful_contacts)} contacts: {', '.join(successful_contacts)}"
                )

            if failed_contacts:
                result_parts.append(
                    f"Failed to store {len(failed_contacts)} contacts: {'; '.join(failed_contacts)}"
                )

            return " ".join(result_parts)

        except json.JSONDecodeError as e:
            return f"Error: Failed to parse contact information as JSON: {str(e)}"
        except KeyError as e:
            return f"Error: Missing required field in contact data: {str(e)}"
        except Exception as e:
            return f"Error: Unexpected error occurred while storing contacts: {str(e)}"
