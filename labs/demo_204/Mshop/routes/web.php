<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductsController;
use App\Http\Controllers\TransactionController;

// Home
Route::get('/', function () {
    return redirect('/products');
});

// Product
Route::group(['prefix' => 'products'], function(){
    //List products.
    Route::get('/', [ProductsController::class, 'listProducts']);
    //Create products.
    Route::get('/create', [ProductsController::class, 'create']);
    //Edit product.
    Route::get('{product_id}/edit',[ProductsController::class, 'edit']);
    //Manage products.
    Route::get('/manage', [ProductsController::class, 'index']);
    //View single product.
    Route::get('{product}/', [ProductsController::class, 'show']);
    //Update product.
    Route::put('{product}/', [ProductsController::class, 'update']);
    //Delete product.
    Route::delete('{product}/',[ProductsController::class, 'destroy']);
    //Buy product.
    Route::post('{product}/buy',[ProductsController::class, 'buy']);
});

// Transaction
Route::group(['prefix' => 'transactions'], function(){
    Route::get('/', [TransactionController::class, 'index']);
    Route::get('{transaction_id}', [TransactionController::class, 'show']);
    Route::get('{user_id}/user', [TransactionController::class, 'listUserTransations']);
});
