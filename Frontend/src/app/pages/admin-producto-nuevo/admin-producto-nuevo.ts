import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import {
  Categoria,
  CategoriasService
} from '../../services/categorias.service';

import {
  ProductoCreate,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-producto-nuevo',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './admin-producto-nuevo.html',
  styleUrl: './admin-producto-nuevo.css'
})
export class AdminProductoNuevo implements OnInit {

  categorias = signal<Categoria[]>([]);

  idCategoria: number | null = null;
  codigo = '';
  nombre = '';
  descripcion = '';
  material = '';
  color = '';
  estilo = '';
  precio: number | null = null;
  imagenUrl = '';

  guardando = signal(false);
  error = signal('');


  constructor(
    private categoriasService: CategoriasService,
    private productosService: ProductosService,
    private router: Router
  ) {}


  ngOnInit(): void {

    this.categoriasService.obtenerCategorias().subscribe({

      next: (categorias) => {
        this.categorias.set(categorias);
      },

      error: () => {
        this.error.set(
          'No se pudieron cargar las categorías'
        );
      }

    });
  }


  guardarProducto(): void {

    if (
      !this.idCategoria ||
      !this.codigo.trim() ||
      !this.nombre.trim() ||
      this.precio === null
    ) {
      this.error.set(
        'Completa categoría, código, nombre y precio'
      );

      return;
    }


    if (this.precio < 0) {

      this.error.set(
        'El precio no puede ser negativo'
      );

      return;
    }


    const producto: ProductoCreate = {

      id_categoria: this.idCategoria,

      codigo: this.codigo.trim(),

      nombre: this.nombre.trim(),

      descripcion:
        this.descripcion.trim() || null,

      material:
        this.material.trim() || null,

      color:
        this.color.trim() || null,

      estilo:
        this.estilo.trim() || null,

      precio: this.precio,

      imagen_url:
        this.imagenUrl.trim() || null
    };


    this.guardando.set(true);
    this.error.set('');


    this.productosService.crearProducto(
      producto
    ).subscribe({

      next: () => {

        this.router.navigate([
          '/admin/productos'
        ]);
      },

      error: (error) => {

        this.guardando.set(false);

        this.error.set(
          error.error?.detail ||
          'No se pudo crear el producto'
        );
      }

    });
  }

}