#!/usr/bin/env python
import sys
import warnings

from sales_contact_finder_crew.crew import SalesContactFinderCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Get inputs from user
    target_company = input("Enter Target Company: ")
    our_product = input("Describe your product: ")
    
    inputs = {
        'target_company': target_company,
        'our_product': our_product
    }
    
    try:
        result = SalesContactFinderCrew().crew().kickoff(inputs=inputs)
        print("\nResults:")
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "target_company": "Example Company",
        "our_product": "AI-powered sales tools"
    }
    try:
        SalesContactFinderCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SalesContactFinderCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "target_company": "Example Company",
        "our_product": "AI-powered sales tools"
    }
    try:
        SalesContactFinderCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [run|train|test|replay] [additional_args...]")
        print("Commands:")
        print("  run                              - Run the crew interactively")
        print("  train <iterations> <filename>    - Train the crew")
        print("  test <iterations> <model_name>   - Test the crew")
        print("  replay <task_id>                 - Replay a specific task")
        sys.exit(1)

    command = sys.argv[1]

    if command == "run":
        run()
    elif command == "train":
        if len(sys.argv) < 4:
            print("Usage: python main.py train <iterations> <filename>")
            sys.exit(1)
        train()
    elif command == "test":
        if len(sys.argv) < 4:
            print("Usage: python main.py test <iterations> <model_name>")
            sys.exit(1)
        test()
    elif command == "replay":
        if len(sys.argv) < 3:
            print("Usage: python main.py replay <task_id>")
            sys.exit(1)
        replay()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
