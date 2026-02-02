<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    // table name
    protected $table = 'products';
    // Primary key
    protected $primaryKey = 'id';
    // Mass Assignment
    protected $fillable = [
        "id",
        "status",
        "name",
        "introduction",
        "photo",
        "price",
        "remain_count",
        "product_type",
    ];
    public function ProductType()
    {
        return $this->hasOne('App\Models\ProductType', 'id', 'product_type');
    }
}
