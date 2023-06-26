from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess
import os

@api_view(['POST'])
def execute_code(request):
    code = request.data.get('code')
    language = request.data.get('language')
    input_text = request.data.get('input')

    if language == 'node':
        # Execute Node.js code and capture the output
        output = execute_nodejs(code, input_text)
    elif language == 'python':
        # Execute Python code and capture the output
        output = execute_python(code, input_text)
    else:
        # Invalid language
        return Response({'error': 'Invalid language'}, status=400)

    return Response({'output': output})

def execute_nodejs(code, input_text):
    # Write the code to a temporary file
    with open('temp.js', 'w') as file:
        file.write(code)

    # Execute the code and capture the output
    try:
        cmd = f'node temp.js'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True)
        output, _ = process.communicate(input=input_text, timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        output = 'Execution timed out.'
    except Exception as e:
        output = str(e)

    # Remove the temporary file
    os.remove('temp.js')

    return output

def execute_python(code, input_text):
    # Convert the input_text to a string
    input_text = str(input_text)

    # Write the code to a temporary file
    with open('temp.py', 'w') as file:
        file.write(code)

    # Execute the code and capture the output
    try:
        output = subprocess.check_output(['python', 'temp.py'], stderr=subprocess.STDOUT, input=input_text, timeout=5, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Remove the temporary file
    os.remove('temp.py')

    return output
