import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from "@angular/router";
import {MainPageComponent} from "./pages/main-page/main-page.component";
import {CreationPageComponent} from "./account/creation-page/creation-page.component";
import {ListPageComponent} from "./account/list-page/list-page.component";
import {LoginCheckComponent} from "./login-check/login-check.component";

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
    path: 'login',
    component: LoginCheckComponent
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
