namespace GoogleSheetsService.Backend
{
    public class ConfigManager
    {
        private readonly string appsettings_path = "appsettings.json";

        private ConfigurationBuilder _configurationBuilder;
        private IConfigurationRoot _config;
        private bool DEBUG = false;

        public ConfigManager()
        {
            _configurationBuilder = new ConfigurationBuilder();
            _configurationBuilder.AddJsonFile(appsettings_path);
            _config = _configurationBuilder.Build();

            string debug = _config.GetValue<string>("DEBUG");

            if (debug == "true")
                DEBUG = true;

        }

        public string GetConnetion()
        {
            if (DEBUG)
                return _config.GetConnectionString("DEBAG_DB");
            return _config.GetConnectionString("DB");
        }

        public string GetConnetionToDataBaseMicroserice()
        {
            return _config.GetConnectionString("DB_MICROSERVICE");
        }

    }
}
