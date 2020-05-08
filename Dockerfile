FROM hasura/graphql-engine:v1.2.1

ENV HASURA_GRAPHQL_ENABLE_CONSOLE="true"
ENV ENABLE_CLOUDSQL_PROXY="true"

CMD graphql-engine \
   --database-url $HASURA_GRAPHQL_DATABASE_URL \
   serve \
   --server-port $PORT \
   --access-key $HASURA_GRAPHQL_ADMIN_SECRET