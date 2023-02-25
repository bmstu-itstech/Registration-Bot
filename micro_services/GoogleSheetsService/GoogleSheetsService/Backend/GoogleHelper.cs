using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;



namespace GoogleSheetsService.Backend
{
    public class GoogleHelper
    {
        private static readonly string[] Scopes = { SheetsService.Scope.Spreadsheets };
        private static readonly string ApplicationName = "baumanbot";

        public static readonly List<string> Sheets = new List<string>();

        private SheetsService service;
        private GoogleCredential credential;

        // private static readonly string SpreadSheetId = Strings.Tokens.GogleToken;


        public GoogleHelper()
        {
            using (var stream = new FileStream("secretes.json", FileMode.Open, FileAccess.Read))
            {
                this.credential = GoogleCredential.FromStream(stream).CreateScoped(Scopes);

            }

            this.service = new SheetsService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName
            });
        }

        public Task<string> InputObject(object inputObject, string sheet_title)
        {
            //В будущем это будет поле, отвечающее за exel_id новой записи
            string exel_id = "";

            return Task.FromResult<string>(exel_id);
        }

        public Task UpdateObject(string sheet_title, string exel_id, object value)
        {
            return Task.Run(() =>
            {
                // Тут должен быть код, запускающий действие по обновлению записи в новом Task 
            });
        }

        public Task AddNewSheet(string sheet_title)
        {
            return Task.Run(() =>
            {
                Sheets.Add(sheet_title);
                // Тут должен быть код, запускающий действие добавления нового листа в новом Task 
            });

        }

        public Task<object> ReadTableString(string sheet_title, string exel_id)
        {
            object get_object = null;

            return Task.FromResult(get_object);
        }

        public Task<List<object>> ReadTableRange(string sheet_title, string exel_id, string range)
        {
            List<object> get_objects = new List<object>();

            return Task.FromResult(get_objects);
        }

    }
}
