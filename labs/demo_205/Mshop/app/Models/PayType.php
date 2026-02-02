<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PayType extends Model
{
    // Table name
    protected $table = 'pay_type';
    // primary key
    protected $primaryKey = 'id';
    // Mass Assignment
    protected $fillable = [
        "type",
    ];
}
