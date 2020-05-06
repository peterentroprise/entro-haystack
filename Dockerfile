FROM hasura/graphql-engine:v1.0.0-beta.6.cli-migrations

WORKDIR /hasura

COPY ./hasura/entrypoint.sh .
COPY ./hasura/migrate.sh .
COPY ./hasura/console.sh .

ADD https://raw.githubusercontent.com/eficode/wait-for/master/wait-for /bin/wait-for
RUN chmod +x /bin/wait-for ./entrypoint.sh ./migrate.sh ./console.sh

ENV ENABLE_MIGRATIONS="true"
ENV ENABLE_CONSOLE="true"
ENV POSTGRES_HOST="postgres"

ENTRYPOINT ["./entrypoint.sh"]

CMD /bin/env


