#!/bin/bash
set -e

get_secrets() {
    aws secretsmanager get-secret-value \
        --secret-id "$SECRET" \
        --query SecretString \
        --output json \
            | jq -r '.|fromjson|to_entries|map("\(.key)=\(.value|tostring)")|.[]'
}

IFS=, read -ra secret_ids <<< $SECRETS_KEYS
# For now disable loading secrets from SM
if false && [[ "$SECRETS_LOAD" = true ]]; then
    for id in "${secret_ids[@]}"
    do
        echo "Loading secrets from ${id}..."
        # source <(get_secrets $id | sh -c "export -p")
        export -p $(get_secrets $id | xargs)
    done
fi

# Please do not log the secrets

set -x
exec "$@"