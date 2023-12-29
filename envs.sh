#!/bin/bash
# Load variables from .env file and export them.

while IFS='=' read -r key value
do
  # Trim leading and trailing whitespace from key and value
  key=$(echo $key | xargs)
  value=$(echo $value | xargs)

  # Replace hyphens with underscores in the key to ensure valid shell variable names
  key=${key//-/_}

  # Handle special characters: Escape asterisks
  value=${value//\*/\\*}

  # Exporting each line as a variable, skipping if line is empty or if it's a comment
  if [[ ! -z "$key" ]] && [[ ! "$key" =~ ^\# ]]; then
    echo "exporting $key as $value"
    export $key="$value"
  fi
done < ".env"
