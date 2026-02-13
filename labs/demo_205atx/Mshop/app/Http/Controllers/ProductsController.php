<?php

namespace App\Http\Controllers;

use App\Models\Product;
use App\Models\User;
use App\Models\Transaction;
use App\Models\PayType;
use App\Models\ProductType;

use Illuminate\Http\Request;

use Illuminate\Support\Facades\DB;
use League\Config\Exception\ValidationException;
use Intervention\Image\Facades\Image;

use Illuminate\Support\Facades\Log;

class ProductsController extends Controller
{
    /**
     * Perform one random change on a random available product.
     *
     * Rules:
     * 1. A random non-deleted product is selected for each change.
     * 2. The change can be:
     *    - a "buy" action that uses the existing purchase routine; OR
     *    - an "add stock" action that increases inventory by a random amount.
     * 3. When current stock (remain_count) is 2 or less, the next action must be "add stock".
     */
    public function autoChangeOne(Request $request)
    {
        $product = Product::where('status', '!=', 'D')
            ->where('name', '!=', '')
            ->inRandomOrder()
            ->first();

        if (!$product) {
            return response()->json([
                'ok' => false,
                'message' => 'No available books found.',
            ], 200);
        }

        $currentStock = $product->remain_count;

        // Decide action according to the rule:
        // - If stock <= 2, we must add stock.
        // - Otherwise, randomly choose between "buy" and "add_stock".
        if ($currentStock <= 2) {
            $action = 'add_stock';
        } else {
            $actions = ['buy', 'add_stock'];
            $action = $actions[array_rand($actions)];
        }

        if ($action === 'buy') {
            // Use existing purchase logic (executeTransaction) to simulate a user buying this book.

            // Choose a random buy count, but not more than current stock and at least 1.
            $maxBuy = max(1, min(3, $currentStock));
            $buyCount = mt_rand(1, $maxBuy);

            // Pick a valid pay type (fallback to 1 if none found).
            $payType = PayType::query()->first();
            $payWith = $payType ? $payType->id : 1;

            $validated = [
                'buy_count' => $buyCount,
                'pay_with'  => $payWith,
            ];

            // Reuse transaction logic; ignore the returned redirect response.
            $this->executeTransaction(new Request($validated), $product, $validated);

            // Reload product to get updated stock.
            $product->refresh();

            return response()->json([
                'ok' => true,
                'action' => 'buy',
                'product_id' => $product->id,
                'product_name' => $product->name,
                'buy_count' => $buyCount,
                'remain_after' => $product->remain_count,
                'message' => "Auto-buy: {$buyCount} copy/copies of \"{$product->name}\" purchased. New stock: {$product->remain_count}.",
            ]);
        }

        // Add stock action.
        $oldStock = $product->remain_count;
        $addAmount = mt_rand(1, 10);
        $product->remain_count = $oldStock + $addAmount;
        $product->save();

        return response()->json([
            'ok' => true,
            'action' => 'add_stock',
            'product_id' => $product->id,
            'product_name' => $product->name,
            'old_stock' => $oldStock,
            'add_amount' => $addAmount,
            'new_stock' => $product->remain_count,
            'message' => "Auto-add stock: inventory for \"{$product->name}\" increased from {$oldStock} to {$product->remain_count} (+{$addAmount}).",
        ]);
    }

    /**
     * List the products for management.
     */
    public function index()
    {
        //
        // Rows per page.
        $row_per_page = 10;

        // Get the products of this page.
        $ProductPaginate = Product::OrderBy('created_at', 'desc')
            ->where('status', '!=', 'D')    // The product can not be deleted.
            ->where('name', '!=', '')       // The name of the book can not be blank.
            ->paginate($row_per_page);

        // Set the title and data for view.
        $binding = [
            'title' => __('shop.product.Book-management'),
            'ProductPaginate'=> $ProductPaginate,
        ];

        // Sent the products data to view.
        return view('products.manageProduct', $binding);
    }

    /**
     * List the products for sell.
     */
    public function listProducts()
    {
        //
        // Rows per page.
        $row_per_page = 10;

        // Get the products of this page.
        $ProductPaginate = Product::OrderBy('updated_at', 'desc')
            ->where('status', 'S')      // for selling.
            ->where('name', '!=', '')   // The name of the book can not be blank.
            ->paginate($row_per_page);  // Pagination.

        // Set the title and data for view.
        $binding = [
            'title' => __('shop.product.Book-list'),
            'ProductPaginate'=> $ProductPaginate,
        ];

        // Sent the products data to view.
        return view('products.listProduct', $binding);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        // Create basic product information
        $product_data = [
            'status'          => 'C',   // In progress
            'name'            => '',    // Product Name
            'introduction'    => '',    // Product Description
            'photo'           => null,  // Product Photo
            'price'           => 0,     // Price
            'remain_count'    => 0,     // Remaining Quantity
        ];

        Product::where('name', '')->Orwhere('price', 0)->delete();

        $Product = Product::create($product_data);

        // Redirecting to Product Editing Page
        return redirect('/products/' . $Product->id . '/edit');
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(Product $product)
    {
        //
        $payTypes = PayType::all();  // Get all pay types.
        $binding = [
            'title' => __('shop.product.Product-details'),
            'Product' => $product,
            'PayTypes' => $payTypes,
        ];
        return view('products.showProduct', $binding);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit($product_id)
    {
        // Get product information.
        $Product = Product::findOrFail($product_id);

        $ProductTypes = ProductType::all(); // Get all product types.

        if (!is_null($Product->photo)) {
            // Set the photo address of product's photo
            $Product->photo = url($Product->photo);
        }

        $binding = [
            'title' => 'Edit Product',
            'Product'=> $Product,
            'ProductTypes' => $ProductTypes,
        ];
        return view('products.editProduct', $binding);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Product $product)
    {

        //Validate
        $validated = $request->validate(rules: [
            'status' => 'required|in:C,S',
            'name' => 'required|string|max:80',
            'introduction' => 'required|string|max:200',
            'price' => 'required|numeric|min:0.1|max:10000|regex:/^\d+(\.\d{1,2})?$/',
            'remain_count' => 'required|integer|min:0',
            'photo' => 'image',
            'product_type' => 'required|min:1',
        ]);

        if (isset($validated['photo'])){
            // Uploaded Image
            $photo = $validated['photo'];
            // File Extension
            $file_extension = $photo->getClientOriginalExtension();

            // Generate Custom Random File Name
            $file_name = uniqid() . '.' . $file_extension;

            // File Relative Path
            $file_relative_path = '/assets/images/' . $file_name;

            // File Location (Public)Relative Position in the Public Directory
            $file_path = public_path($file_relative_path);

            // Crop Image
            $image = Image::make($photo)->fit(359, 522)->save($file_path);
            // Set Relative Position of Image File
            $validated['photo'] = $file_relative_path;
        }
        else {
            if ($product->photo) {
                $validated['photo'] = $product->photo;

            }
            else{
                $validated['photo'] = '/assets/images/defaultphoto.png';
            }
        }

        $product->update($validated);

        // Return to the product edit page.

        return redirect('/products/manage');
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Product $product)
    {
        //
        //$product->delete();
        // If the value of 'status' is 'D', the book will be deleted from the inventory.
        $product->status = 'D';

        $product->save();

        return redirect('/products/manage');
    }

    /**
     * Process the products purchase.
     */
    public function buy(Request $request, Product $product)
    {
        try {
            //Validate
            $validated = $request->validate(rules: [
                'buy_count' => 'required|integer|min:1',
                'pay_with' => 'required|integer|min:1',
            ]);
        } catch(ValidationException $e) {

            return redirect('/products/' . $product->id)
                ->withErrors($validated)
                ->withInput();
        }

        /**
         * If $OnlineSchemaChange is true, execute function $this->executeTransactionWithRetry(...) to prevent from the
         * error 'Error 8028: Information schema is changed during the execution of the statement' by retry for purchase transaction.
         * If $OnlineSchemaChange is false, execute function $this->executeTransaction(...) for purchase transaction without retry.
         */
        $OnlineSchemaChange = false;

        if($OnlineSchemaChange) {

            //Execute the logic of purchase transaction.
            return $this->executeTransactionWithRetry($request, $product, $validated);
        } else {
            //Use recursive functions to handle retry logic of purchase transaction.
            return $this->executeTransaction($request, $product, $validated);

        }
    }

    private function executeTransaction($request, $product, $validated, $retryCount = 0)
    {
        try {
            // Retrieve Login Member Information
            $user_id = 1; //Hard code
            $User = User::findOrFail($user_id);

            // Transaction Start
            DB::beginTransaction();

            // Retrieve Product Information
            $product = Product::findOrFail($product->id);

            // Purchase Quantity
            $buy_count = $validated['buy_count'];

            // Pay type
            $pay_type = $validated['pay_with'];

            // Remaining Quantity After Purchase
            $remain_count_after_buy = $product->remain_count - $buy_count;
            if ($remain_count_after_buy < 0) {
                // Remaining quantity after purchase is less than 0, insufficient to sell to the user
                throw new \Exception('Insufficient quantity of goods, unable to purchase.');
            }

            // Record Remaining Quantity After Purchase
            $product->remain_count = $remain_count_after_buy;
            $product->save();

            // Total Amount: Total Purchase Quantity * Product Price
            $total_price = $buy_count * $product->price;

            $transaction_data = [
                'user_id'        => $User->id,
                'product_id'     => $product->id,
                'price'          => $product->price,
                'buy_count'      => $buy_count,
                'total_price'    => $total_price,
                'pay_type'       => $pay_type,
            ];

            // Create Transaction Details
            $transaction = Transaction::create($transaction_data);

            // Transaction End
            DB::commit();

            // Return Purchase Success Message
            $message = [
                'msg' => [
                    __('shop.Message.Purchase-successfully'),
                ],
            ];
            return redirect()
                ->to('/transactions/' . $transaction->id)
                ->withErrors($message);

        } catch (\Exception $exception) {

            // Rollback Original Transaction Status
            DB::rollBack();

            // Return Error Message
            $error_message = [
                'msg' => [
                    $exception->getMessage(),
                ],
            ];
            return redirect()
                ->back()
                ->withErrors($error_message)
                ->withInput();
        }
    }

    private function executeTransactionWithRetry($request, $product, $validated, $retryCount = 0)
    {
        try {
            // Retrieve Login Member Information
            $user_id = 1; //Hard code
            $User = User::findOrFail($user_id);

            // Transaction Start
            DB::beginTransaction();

            // Debug
            Log::info("Trx begin!");

            // Retrieve Product Information
            $product = Product::findOrFail($product->id);

            // Purchase Quantity
            $buy_count = $validated['buy_count'];

            // Pay type
            $pay_type = $validated['pay_with'];

            // Remaining Quantity After Purchase
            $remain_count_after_buy = $product->remain_count - $buy_count;
            if ($remain_count_after_buy < 0) {
                // Remaining quantity after purchase is less than 0, insufficient to sell to the user
                throw new \Exception(__('shop.Message.Insufficient-goods'));
            }

            // Record Remaining Quantity After Purchase
            $product->remain_count = $remain_count_after_buy;
            $product->save();

            // Total Amount: Total Purchase Quantity * Product Price
            $total_price = $buy_count * $product->price;

            $transaction_data = [
                'user_id'        => $User->id,
                'product_id'     => $product->id,
                'price'          => $product->price,
                'buy_count'      => $buy_count,
                'total_price'    => $total_price,
                'pay_type'       => $pay_type,
            ];

            // Create Transaction Details
            $transaction = Transaction::create($transaction_data);

            // Transaction End
            DB::commit();

            // Return Purchase Success Message
            $message = [
                'msg' => [
                    __('shop.Message.Purchase-successfully'),
                ],
            ];
            return redirect()
                ->to('/transactions/' . $transaction->id)
                ->withErrors($message);

        } catch (\Exception $exception) {
            // Rollback Original Transaction Status
            DB::rollBack();
            // Debug
            Log::info($exception->getMessage());
            // Check if it is a specific error and retry (maximum 3 retries).
            if (strpos($exception->getMessage(), 'General error: 8028 Information schema is changed during the execution of the statement') !== false
                && $retryCount < 3) {
                // Debug
                Log::info($exception->getMessage());
                // Try again after a short wait.
                usleep(100000); // 100ms
                return $this->executeTransactionWithRetry($request, $product, $validated, $retryCount + 1);
            }

            // Return Error Message
            $error_message = [
                'msg' => [
                    $exception->getMessage(),
                ],
            ];
            return redirect()
                ->back()
                ->withErrors($error_message)
                ->withInput();
        }
    }
}
