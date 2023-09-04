import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {CarouselModule} from "ngx-bootstrap/carousel";

import { AppComponent } from './app.component';
import { CreationPageComponent } from './account/creation-page/creation-page.component';
import { ListPageComponent } from './account/list-page/list-page.component';
import { HeaderComponent } from "./header/header.component";
import { MainPageComponent } from './pages/main-page/main-page.component';
import { AppRoutingModule } from './app-routing.module';
import { LoginCheckComponent } from './login-check/login-check.component';
import { FormsModule } from "@angular/forms";

@NgModule({
  declarations: [
    AppComponent,
    CreationPageComponent,
    ListPageComponent,
    HeaderComponent,
    MainPageComponent,
    LoginCheckComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    CarouselModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent, MainPageComponent, HeaderComponent, ListPageComponent, CreationPageComponent]
})
export class AppModule { }
