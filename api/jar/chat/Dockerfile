FROM shoothzj/jdk13base:0.0.8

COPY ./chatDBServer-0.0.1-SNAPSHOT.jar /usr/src/chatDBServer-0.0.1-SNAPSHOT.jar

EXPOSE 8000

WORKDIR /usr/src/

CMD ["java", "-jar", "chatDBServer-0.0.1-SNAPSHOT.jar"]

