import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar-main/navbar-main.component';
import { MainPageComponent } from './pages/main-page/main-page.component';
import { AppRoutingModule } from './app-routing.module';
import { PersonalPageComponent } from './pages/personal-page/personal-page.component';
import { NavbarPersonalComponent } from './navbar-personal/navbar-personal.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    MainPageComponent,
    PersonalPageComponent,
    NavbarPersonalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent, NavbarComponent, MainPageComponent, PersonalPageComponent]
})
export class AppModule { }
