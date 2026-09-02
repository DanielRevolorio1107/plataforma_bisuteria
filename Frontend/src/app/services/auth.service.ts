import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface LoginRequest {
  usuario: string;
  password: string;
}


export interface TokenResponse {
  access_token: string;
  token_type: string;
}


interface JwtPayload {
  exp?: number;
  sub?: string;
  usuario?: string;
}


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private http = inject(HttpClient);

  private apiUrl =
    'http://127.0.0.1:8000/auth/login';


  login(
    datos: LoginRequest
  ): Observable<TokenResponse> {

    return this.http.post<TokenResponse>(
      this.apiUrl,
      datos
    );
  }


  guardarToken(token: string): void {

    localStorage.setItem(
      'admin_token',
      token
    );
  }


  obtenerToken(): string | null {

    return localStorage.getItem(
      'admin_token'
    );
  }


  cerrarSesion(): void {

    localStorage.removeItem(
      'admin_token'
    );
  }


  estaAutenticado(): boolean {

    const token = this.obtenerToken();

    if (!token) {
      return false;
    }


    if (this.tokenExpirado(token)) {

      this.cerrarSesion();

      return false;
    }


    return true;
  }


  private tokenExpirado(
    token: string
  ): boolean {

    try {

      const partes = token.split('.');

      if (partes.length !== 3) {
        return true;
      }


      const payloadBase64 =
        partes[1]
          .replace(/-/g, '+')
          .replace(/_/g, '/');


      const relleno =
        payloadBase64.padEnd(
          Math.ceil(payloadBase64.length / 4) * 4,
          '='
        );


      const binario =
        atob(relleno);


      const bytes =
        Uint8Array.from(
          binario,
          caracter => caracter.charCodeAt(0)
        );


      const json =
        new TextDecoder().decode(bytes);


      const payload: JwtPayload =
        JSON.parse(json);


      if (!payload.exp) {
        return true;
      }


      const fechaActual =
        Math.floor(
          Date.now() / 1000
        );


      return payload.exp <= fechaActual;

    } catch {

      return true;
    }
  }

}