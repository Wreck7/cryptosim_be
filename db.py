from supabase import create_client


# url = 'https://kgrpxirvwdgnqsmwgnff.supabase.co' # team database
# key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtncnB4aXJ2d2RnbnFzbXdnbmZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3NzU1OTcsImV4cCI6MjA2NjM1MTU5N30.2GKEl_lkltL4IEc9Y0S_QrM9kzT3tzVRFxZ4MlAPx_8'

url = 'https://yfyxmprbbtcmkzqxhsgp.supabase.co' # test database
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlmeXhtcHJiYnRjbWt6cXhoc2dwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzOTY5NzcsImV4cCI6MjA2Njk3Mjk3N30.pgOhI9vJ4RegmJxitcvewYrHfuXdOGxLkPDFob069Rg'

db = create_client(url, key)