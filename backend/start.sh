#!/bin/sh

# Make sure DATABASE_URL is visible
echo "📦 DATABASE_URL: $DATABASE_URL"

# Run Prisma
prisma generate

# Start the app
uvicorn main:app --host 0.0.0.0 --port 10000
