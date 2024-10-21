# Use the official .NET 8 SDK image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

# Copy the published output to the container
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["web-api/web-api.csproj", "web-api/"]
RUN dotnet restore "web-api/web-api.csproj"
COPY . .
WORKDIR "/src/web-api"
RUN dotnet build "web-api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "web-api.csproj" -c Release -o /app/publish

# Final stage/image
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "web-api.dll"]
