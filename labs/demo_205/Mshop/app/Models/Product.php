<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Casts\Attribute;

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

    /**
     * Get the photo URL with proper prefix for proxy environments.
     */
    protected function photoUrl(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->attributes['photo'] ? url($this->attributes['photo']) : '',
        );
    }

    public function ProductType()
    {
        return $this->hasOne('App\Models\ProductType', 'id', 'product_type');
    }
}
