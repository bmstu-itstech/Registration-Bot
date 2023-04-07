using DataBaseService.backend.Types;
using DataBaseService.Models;
using DataBaseService.Protos;

namespace DataBaseService.Backend.Types
{
    public class OrgUser
    {
        public int Id { get; set; }
        public string Org_title { get; set; }
        public string Org_description { get; set; }
        public string Admin_contact { get; set; }

        public static Task<List<MyBot>> GetUserBots(int user_id)
        {
            return Task.Run(() =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {

                    List<MyBot> userBots = new List<MyBot>();

                    var bots = db.Bots.Where(bot => bot.Owner == user_id).ToList();
                    Console.WriteLine(bots.Count);


                    foreach(var bot in bots)
                    {
                        userBots.Add(new MyBot
                        {
                            bot_survey_id = bot.Id,
                            google_token = bot.GoogleToken,
                            tg_token = bot.TgToken,
                            owner = bot.Owner,
                            Id = bot.Id,
                            
                        });
                    }

                    return userBots;
                }

            });
        }
        public static Task Registration(Protos.User user_request)
        {
            return Task.Run(async () =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {
                    var user = new Models.User()
                    {
                        Owner = user_request.Contact,
                        Title = user_request.Title,
                        Description = user_request.Description,
                    };

                    await db.Users.AddAsync(user);

                    await db.SaveChangesAsync();
                }
            });
        }

        public static Task<OrgUser> GetUser(int user_id)
        {
            return Task.Run(() =>
            {
                using (RegistrationBotContext db = new RegistrationBotContext())
                {
                    var user = db.Users.Where(user => user.Id == user_id).First();

                    return new OrgUser()
                    {
                        Id = user.Id,
                        Org_description = user.Description,
                        Org_title = user.Title,
                        Admin_contact = user.Owner
                    };
                }
            });
        }
    }
}
