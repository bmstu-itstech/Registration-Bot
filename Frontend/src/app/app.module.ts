import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {CarouselModule} from "ngx-bootstrap/carousel";
import { PopoverModule } from 'ngx-bootstrap/popover';
import {ModalModule} from "ngx-bootstrap/modal";
import {NgxGraphModule} from "@swimlane/ngx-graph";
import {NgxChartsModule} from "@swimlane/ngx-charts";
import {HttpClientModule} from "@angular/common/http";

import { AppComponent } from './app.component';
import { CreationPageComponent } from './pages/creation-page/creation-page.component';
import { ListPageComponent } from './pages/list-page/list-page.component';
import { HeaderComponent } from "./header/header.component";
import { MainPageComponent } from './pages/main-page/main-page.component';
import { AppRoutingModule } from './app-routing.module';
import { SettingsPageComponent } from './pages/settings-page/settings-page.component';
import { LoginCheckComponent } from './login-check/login-check.component';
import { FormsModule } from "@angular/forms";
import {JsonHandlerService} from "./service/json-handler.service";

@NgModule({
  declarations: [
    AppComponent,
    CreationPageComponent,
    ListPageComponent,
    HeaderComponent,
    MainPageComponent,
    SettingsPageComponent,
    LoginCheckComponent,
    TextBlockPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    CarouselModule.forRoot(),
    PopoverModule.forRoot(),
    ModalModule.forRoot(),
    HttpClientModule,
    NgxGraphModule,
    NgxChartsModule
  ],
  providers: [JsonHandlerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
