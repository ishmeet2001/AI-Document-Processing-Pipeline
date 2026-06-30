from application.pipelines.llm_pipeline import create_agent_instance,format_template
from infrastructure.CLI.main import read_files
from config import COMMAND
from domain.prompts.human_instructions import human_template
from domain.schema.invoice import Invoice, ItemDetails
from domain.schema.clinical import PatientReferral, ClinicalNoteDetails

# Initialize both agents at startup
invoice_agent = create_agent_instance(Invoice, ItemDetails)
clinical_agent = create_agent_instance(PatientReferral, ClinicalNoteDetails)

print("=====Welcome to Unstructured Data Pipeline======")
print("For help type Commands")

while(True):
    command=input()
    if command.strip()=="Commands":
        print("Exit")
        print("process [invoice|clinical] <input_path> --db <output_db_path>")
        print("Default command pattern: " + str(COMMAND))
    elif command.strip()=="Exit":
        break
    else:
        command_str = command.strip()
        
        if not command_str.lower().startswith("process"):
            print("Invalid command. First argument must be 'process'")
            continue
        
        if "--db" not in command_str:
            print("Invalid command format. Missing '--db' flag")
            continue
        
        try:
            parts = command_str.split("--db")
            
            if len(parts) != 2:
                print("Invalid command format. Expected: process [schema_type] <input_path> --db <output_db_path>")
                continue
            
            input_part = parts[0].strip()
            if input_part.lower().startswith("process"):
                args_part = input_part[7:].strip()  
            else:
                print("Invalid command format.")
                continue
            
            # Parse schema_type and input_path (backward compatible: defaults to invoice)
            schema_type = "invoice"
            input_path = args_part
            
            if args_part.lower().startswith("invoice "):
                schema_type = "invoice"
                input_path = args_part[8:].strip()
            elif args_part.lower().startswith("clinical "):
                schema_type = "clinical"
                input_path = args_part[9:].strip()
            
            # Extract output database path
            output_db_path = parts[1].strip() if parts[1].strip() else None
            
            if not input_path:
                print("Invalid command format. Input path is required.")
                continue
            
            # Strip quotes if present
            input_path = input_path.strip('"').strip("'")
            if output_db_path:
                output_db_path = output_db_path.strip('"').strip("'")
            
            print(f"Mode: {schema_type.upper()}")
            print(f"Input path: {input_path}")
            print(f"Output DB path: {output_db_path}")
            
            # Select the appropriate agent
            react_agent = clinical_agent if schema_type == "clinical" else invoice_agent
            
            # Read and validate files
            file_contents = read_files([input_path] if type(input_path) == str else input_path)
            
            if file_contents:
                print(f"Successfully processed {len(file_contents)} file(s)")
                
                for content in file_contents:
                    print("\nProcessing file content with LangChain agent...")

                    formatted_template=human_template.format(
                        content=content,
                        output_db_path=output_db_path,
                    )
            
                    response = react_agent.invoke(
                        {"messages":formatted_template},
                        config={"configurable": {"thread_id": "1"}}
                    )
                    
                    print("Processing complete.")
            else:
                print("No valid files to process.")
        except Exception as e:
            print(f"Error processing files: {str(e)}")

