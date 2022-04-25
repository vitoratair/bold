import { IProfile } from './../../views/shared/models/users.model';
import { Component, OnInit} from '@angular/core';
import { INavData } from '@coreui/angular';
import { navItems as menus } from '../../_nav';


@Component({
  selector: 'app-dashboard',
  templateUrl: './default-layout.component.html'
})
export class DefaultLayoutComponent implements OnInit {
  public sidebarMinimized = false;
  public navItems: INavData[] = [];

  constructor() {

  }

  ngOnInit() {

      this.navItensReplacement();
  }

  navItensReplacement() {
    this.navItems = [...menus];
  }

  toggleMinimize(e) {
    this.sidebarMinimized = e;
  }
}
