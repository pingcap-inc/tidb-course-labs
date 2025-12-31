<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Transaction extends Model
{
    // Table name
    protected $table = 'transactions';
    // primary key
    protected $primaryKey = 'id';
    // Mass Assignment
    protected $fillable = [
        "id",
        "user_id",
        "product_id",
        "price",
        "buy_count",
        "total_price",
    ];
    public function Product()
    {
        return $this->hasOne('App\Models\Product', 'id', 'product_id');
    }
    public function User()
    {
        return $this->hasOne('App\Models\User', 'id', 'user_id');
    }
}
