FROM shoothzj/jdk13base:0.0.8
COPY ./logindbServer-0.0.1-SNAPSHOT.jar /usr/src/logindbServer-0.0.1-SNAPSHOT.jar
EXPOSE 8000
WORKDIR /usr/src/
CMD ["java", "-jar", "logindbServer-0.0.1-SNAPSHOT.jar"]
