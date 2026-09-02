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

import {
  UploadsService
} from '../../services/uploads.service';


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

  archivoImagen: File | null = null;

  guardando = signal(false);
  error = signal('');


  constructor(
    private categoriasService: CategoriasService,
    private productosService: ProductosService,
    private uploadsService: UploadsService,
    private router: Router
  ) {}


  ngOnInit(): void {

    this.categoriasService
      .obtenerCategorias()
      .subscribe({

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


  seleccionarImagen(
    event: Event
  ): void {

    const input =
      event.target as HTMLInputElement;

    const archivo =
      input.files?.[0];


    if (!archivo) {
      this.archivoImagen = null;
      return;
    }


    const tiposPermitidos = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ];


    if (
      !tiposPermitidos.includes(
        archivo.type
      )
    ) {

      this.error.set(
        'La imagen debe ser JPG, PNG o WEBP'
      );

      input.value = '';
      this.archivoImagen = null;

      return;
    }


    if (
      archivo.size >
      5 * 1024 * 1024
    ) {

      this.error.set(
        'La imagen no puede superar los 5 MB'
      );

      input.value = '';
      this.archivoImagen = null;

      return;
    }


    this.archivoImagen = archivo;
    this.error.set('');
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


    this.guardando.set(true);
    this.error.set('');


    if (this.archivoImagen) {

      this.subirImagenYCrearProducto();

    } else {

      this.crearProducto(null);

    }
  }


  private subirImagenYCrearProducto(): void {

    if (!this.archivoImagen) {
      this.crearProducto(null);
      return;
    }


    this.uploadsService
      .subirImagen(this.archivoImagen)
      .subscribe({

        next: (respuesta) => {

          this.crearProducto(
            respuesta.imagen_url
          );
        },

        error: (error) => {

          this.guardando.set(false);

          this.error.set(
            error.error?.detail ||
            'No se pudo subir la imagen'
          );
        }

      });
  }


  private crearProducto(
    imagenUrl: string | null
  ): void {

    const producto: ProductoCreate = {

      id_categoria:
        this.idCategoria!,

      codigo:
        this.codigo.trim(),

      nombre:
        this.nombre.trim(),

      descripcion:
        this.descripcion.trim() || null,

      material:
        this.material.trim() || null,

      color:
        this.color.trim() || null,

      estilo:
        this.estilo.trim() || null,

      precio:
        this.precio!,

      imagen_url:
        imagenUrl
    };


    this.productosService
      .crearProducto(producto)
      .subscribe({

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