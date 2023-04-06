using DataBaseService.Models;

namespace DataBaseService.backend.Types
{
    public class MyBot
    {
        public int Id { get; set; }
        public string tg_token { get; set; }
        public string google_token { get; set; }
        public int owner { get; set; }
        public int bot_survey_id { get; set; }


        public static Task AddNewBot(int bot_survey_id, int owner)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {
                    var bot = new Bot
                    {
                        BotId = bot_survey_id,
                        Owner = owner,
                        TgToken = "",
                        GoogleToken = ""
                      
                    };

                    await  db.Bots.AddAsync(bot);
                    db.Users.Where(user => user.Id == owner).First().Bots.Add(bot);

                    await db.SaveChangesAsync();

                }
            });
        }
    }
}
