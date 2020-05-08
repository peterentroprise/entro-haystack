FROM hasura/graphql-engine:v1.2.1

CMD graphql-engine \
   --database-url $HASURA_GRAPHQL_DATABASE_URL \
   serve \
   --server-port $PORT