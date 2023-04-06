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

    public virtual DbSet<Bot> Bots { get; set; }

    public virtual DbSet<User> Users { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        var _config = new ConfigManager();


        Console.WriteLine(_config.GetConnetion());
        optionsBuilder.UseNpgsql(_config.GetConnetion());
    }


    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasPostgresExtension("pg_catalog", "adminpack");

        modelBuilder.Entity<Bot>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("Bots_pkey");

            entity.Property(e => e.BotId).HasColumnName("bot_id");
            entity.Property(e => e.GoogleToken)
                .HasMaxLength(255)
                .HasColumnName("google_token");
            entity.Property(e => e.Owner).HasColumnName("owner");
            entity.Property(e => e.TgToken)
                .HasMaxLength(255)
                .HasColumnName("tg_token");

            entity.HasOne(d => d.OwnerNavigation).WithMany(p => p.Bots)
                .HasForeignKey(d => d.Owner)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("owner");
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("Users_pkey");

            entity.Property(e => e.Description).HasMaxLength(255);
            entity.Property(e => e.Owner).HasMaxLength(255);
            entity.Property(e => e.Title).HasMaxLength(255);
        });
        modelBuilder.HasSequence<int>("bot_id_sequence");

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
