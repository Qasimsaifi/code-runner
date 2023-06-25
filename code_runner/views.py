from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CodeSnippetSerializer
from .models import CodeSnippet
import io
import sys

class CodeSnippetViewSet(ModelViewSet):
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer

    def execute_code(self, code, user_input):
        try:
            # Create a namespace dictionary for execution
            namespace = {}

            # Redirect the standard output to a variable
            stdout = io.StringIO()
            sys.stdout = stdout

            # Redirect the standard input to a variable
            stdin = io.StringIO(user_input)
            sys.stdin = stdin

            # Execute the code within the namespace
            exec(code, namespace)

            # Capture the output
            output = stdout.getvalue()
            errors = None
        except Exception as e:
            # Capture any errors that occur during code execution
            output = ''
            errors = str(e)
        finally:
            # Restore the standard output, standard input, and clear the namespace
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__
            namespace.clear()

        return output, errors

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user input from the serializer
        user_input = serializer.validated_data.get('user_input', '')

        # Execute the code with user input
        output, errors = self.execute_code(serializer.validated_data['code'], user_input)

        response_data = {
            'code': serializer.validated_data['code'],
            'output': output,
            'errors': errors,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
