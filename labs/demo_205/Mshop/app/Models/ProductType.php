<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ProductType extends Model
{
    // Table name
    protected $table = 'product_type';
    // primary key
    protected $primaryKey = 'id';
    // Mass Assignment
    protected $fillable = [
        "type",
    ];
}
