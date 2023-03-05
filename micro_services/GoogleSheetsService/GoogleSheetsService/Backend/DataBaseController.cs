namespace GoogleSheetsService.Backend
{

    // В ближайшем будущем будет локальная база данных
    // У каждого бота своя table_id 
    //
    public class DataBaseController
    {
        private string host;
        private string user;
        private string password;
        private int port;
        private string data_base_name;

        public DataBaseController(string host, string user, string password, int port, string data_base_name)
        {
            this.host = host;
            this.user = user;
            this.password = password;
            this.port = port;
            this.data_base_name = data_base_name;
        }

        public async Task<string> Get_bot_sheetId(int bot_id)
        {
            // Код заглушка, будет возвращать sheet_id конкретного бота
            // здесь будет вызвано обращение к микросервису, отвечающему за работу с базой данных

            // Test return value
            string bot_sheet = "1uLArDR2des-o07aUvK8sG7mXNPLsm6tA2nLLWgph9t0";

            return await Task.FromResult(bot_sheet);
        }
    }
}
