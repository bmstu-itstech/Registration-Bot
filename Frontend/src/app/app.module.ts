import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CreationPageComponent } from './account/creation-page/creation-page.component';
import { ListPageComponent } from './account/list-page/list-page.component';
import { HeaderComponent } from './account/header/header.component';
import { NavbarComponent } from './navbar-main/navbar-main.component';
import { MainPageComponent } from './pages/main-page/main-page.component';
import { AppRoutingModule } from './app-routing.module';
import { PersonalPageComponent } from './pages/personal-page/personal-page.component';
import { NavbarPersonalComponent } from './navbar-personal/navbar-personal.component';
import { SettingsPageComponent } from './account/settings-page/settings-page.component';

@NgModule({
  declarations: [
    AppComponent,
    CreationPageComponent,
    ListPageComponent,
    HeaderComponent,
    NavbarComponent,
    MainPageComponent,
    PersonalPageComponent,
    NavbarPersonalComponent,
    SettingsPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent, NavbarComponent, MainPageComponent, PersonalPageComponent]
})
export class AppModule { }
