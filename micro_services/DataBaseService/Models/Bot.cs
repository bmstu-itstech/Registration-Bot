using System;
using System.Collections.Generic;

namespace DataBaseService.Models;

public partial class Bot
{
    public int Id { get; set; }

    public string TgToken { get; set; } = null!;

    public string GoogleToken { get; set; } = null!;

    public int Owner { get; set; }

    public int BotId { get; set; }

    public virtual User OwnerNavigation { get; set; } = null!;
}
