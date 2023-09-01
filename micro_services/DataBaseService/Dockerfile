FROM mcr.microsoft.com/dotnet/sdk:6.0

WORKDIR /DataBaseService
COPY . .

RUN dotnet restore
RUN dotnet dev-certs https --clean && dotnet dev-certs https --trust

ENV ASPNETCORE_URLS="http://+:7000;http://+:7001"

EXPOSE 7000

ENTRYPOINT ["dotnet", "run"]