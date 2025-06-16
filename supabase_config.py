from supabase import create_client

url ="https://qrldvyhiorjjaiiyoboo.supabase.co" # 🔁 Replace with your Supabase API key
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFybGR2eWhpb3JqamFpaXlvYm9vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTkwOTc1NCwiZXhwIjoyMDY1NDg1NzU0fQ.Je_nVqPOR0mTabr8vzE6K4oPCnywWZpjvgz7u-heWJg"
supabase = create_client(url, key)