using System;
using System.Collections.Generic;
using DataBaseService.Backend.Config;
using Microsoft.EntityFrameworkCore;

namespace DataBaseService.Models;

public partial class RegistrationBotContext : DbContext
{
    public RegistrationBotContext()
    {
    }

    public RegistrationBotContext(DbContextOptions<RegistrationBotContext> options)
        : base(options)
    {
    }

    public virtual DbSet<User> Users { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        var _config = new ConfigManager();


        optionsBuilder.UseNpgsql(_config.GetConnetion());
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasPostgresExtension("pg_catalog", "adminpack");

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("Users_pkey");

            entity.Property(e => e.Description).HasMaxLength(255);
            entity.Property(e => e.Owner).HasMaxLength(255);
            entity.Property(e => e.Title).HasMaxLength(255);
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
