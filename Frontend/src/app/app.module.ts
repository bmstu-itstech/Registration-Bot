import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {CarouselModule} from "ngx-bootstrap/carousel";
import { PopoverModule } from 'ngx-bootstrap/popover';

import { AppComponent } from './app.component';
import { CreationPageComponent } from './account/creation-page/creation-page.component';
import { ListPageComponent } from './account/list-page/list-page.component';
import { HeaderComponent } from "./header/header.component";
import { MainPageComponent } from './pages/main-page/main-page.component';
import { AppRoutingModule } from './app-routing.module';

import { PersonalPageComponent } from './pages/personal-page/personal-page.component';
import { NavbarPersonalComponent } from './navbar-personal/navbar-personal.component';
import { SettingsPageComponent } from './account/settings-page/settings-page.component';

import { LoginCheckComponent } from './login-check/login-check.component';
import { FormsModule } from "@angular/forms";


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
    SettingsPageComponent,
    LoginCheckComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    CarouselModule.forRoot(),
    PopoverModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent, MainPageComponent, HeaderComponent, ListPageComponent, CreationPageComponent]
})
export class AppModule { }
