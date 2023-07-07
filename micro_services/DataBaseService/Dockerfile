FROM mcr.microsoft.com/dotnet/nightly/sdk:6.0

WORKDIR /DataBaseService
COPY . .

RUN dotnet restore
RUN dotnet dev-certs https --clean && dotnet dev-certs https --trust

ENV ASPNETCORE_URLS="http://+:5292"

ENTRYPOINT ["dotnet", "run"]