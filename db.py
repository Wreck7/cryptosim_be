from supabase import create_client


url = 'https://yfyxmprbbtcmkzqxhsgp.supabase.co'  # test database
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlmeXhtcHJiYnRjbWt6cXhoc2dwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzOTY5NzcsImV4cCI6MjA2Njk3Mjk3N30.pgOhI9vJ4RegmJxitcvewYrHfuXdOGxLkPDFob069Rg'

db = create_client(url, key)
