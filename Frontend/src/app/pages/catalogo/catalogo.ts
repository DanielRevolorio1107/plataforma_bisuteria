import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-catalogo',
  imports: [RouterLink],
  templateUrl: './catalogo.html',
  styleUrl: './catalogo.css'
})
export class Catalogo implements OnInit {

  productos = signal<Producto[]>([]);
  cargando = signal(true);
  error = signal('');

  constructor(
    private productosService: ProductosService
  ) {}

  ngOnInit(): void {
    this.productosService.obtenerProductos().subscribe({

      next: (datos) => {
        this.productos.set(datos);
        this.cargando.set(false);
      },

      error: () => {
        this.error.set('No se pudieron cargar los productos');
        this.cargando.set(false);
      }

    });
  }
}