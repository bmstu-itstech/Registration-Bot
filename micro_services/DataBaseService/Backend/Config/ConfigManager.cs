namespace DataBaseService.Backend.Config
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

        public string? GetConnetion()
        {
            if (DEBUG)
                return _config.GetConnectionString("DEBUG_DB");
            return _config.GetConnectionString("DB");
        }

        public string GetBotConnetion(int data_base_id)
        {
            string base_conn = _config.GetConnectionString("DB");

            if (DEBUG)
                base_conn = _config.GetConnectionString("DEBUG_DB");

            base_conn = base_conn.Replace(_config.GetValue<string>("DATA_BASE_NAME"), $"BOT_{data_base_id}");

            return base_conn;

        }
    }
}
