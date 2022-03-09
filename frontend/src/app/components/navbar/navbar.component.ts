import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(public authService: AuthService) { }

  token:string | null | undefined; 
  ver = false

  ngOnInit() {
    // const userJson = localStorage.getItem('currentUser');
    // this.currentUser = userJson !== null ? JSON.parse(userJson) : new User();

    this.token = this.authService.getToken()
    String(this.token)

    setTimeout(() => {
      if(this.token == "undefined") {
        this.ver=true;
      }
    }, 500);

  }

}
