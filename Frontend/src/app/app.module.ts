import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CreationPageComponent } from './account/creation-page/creation-page.component';
import { ListPageComponent } from './account/list-page/list-page.component';
import { HeaderComponent } from './account/header/header.component';

@NgModule({
  declarations: [
    AppComponent,
    CreationPageComponent,
    ListPageComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
