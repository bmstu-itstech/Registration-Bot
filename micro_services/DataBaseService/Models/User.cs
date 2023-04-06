using System;
using System.Collections.Generic;

namespace DataBaseService.Models;

public partial class User
{
    public int Id { get; set; }

    public string Title { get; set; } = null!;

    public string Description { get; set; } = null!;

    public string Owner { get; set; } = null!;

    public virtual ICollection<Bot> Bots { get; } = new List<Bot>();
}
