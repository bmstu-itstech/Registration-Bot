FROM mcr.microsoft.com/dotnet/sdk:6.0

WORKDIR /GoogleSheetsService
COPY . .

RUN dotnet restore
RUN dotnet dev-certs https --clean && dotnet dev-certs https --trust

ENV ASPNETCORE_URLS="https://+:8001;http://+:8000"

ENTRYPOINT ["dotnet", "run"]