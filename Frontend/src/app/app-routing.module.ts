import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from "@angular/router";
import {MainPageComponent} from "./pages/main-page/main-page.component";
import {CreationPageComponent} from "./account/creation-page/creation-page.component";
import {ListPageComponent} from "./account/list-page/list-page.component";
import {LoginCheckComponent} from "./login-check/login-check.component";
import {SettingsPageComponent} from "./account/settings-page/settings-page.component";
import {TextBlockPageComponent} from "./account/text-block-page/text-block-page.component";

const routes: Routes = [
  {
    path: '',
    component: MainPageComponent
  },
  {
    path: 'creation',
    component: CreationPageComponent
  },
  {
    path: 'list',
    component: ListPageComponent
  },
  {
    path: 'settings',
    component: SettingsPageComponent
  },
  {
    path: 'login',
    component: LoginCheckComponent
  },
  {
    path: 'add_text_block',
    component: TextBlockPageComponent
  }
]

@NgModule({
  declarations: [],
  imports: [
    CommonModule, RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
