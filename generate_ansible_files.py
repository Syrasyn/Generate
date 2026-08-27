import generate_tla_yml as gen_tla
import generate_tla_units_yml as gen_units

def main():
    print('''
    THIS TOOL GENERATES THE REQUIRED YAML FILES FOR THE SWITCH-CONFIG ANSIBLE PLAYBOOKS.
    FOLLOW THE PROMPTS TO ENTER THE REQUIRED INFORMATION FOR THE NEW DEPLOYMENT.
    ''')
    gen_tla.main()
    gen_units.main()

    print('''
    YAML FILES GENERATED SUCCESSFULLY.
    ''')

if __name__ == "__main__":
    main()
    