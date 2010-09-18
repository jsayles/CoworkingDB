Directory::Application.routes.draw do
  resources :places
  resources :spaces

  match 'test' => 'directory#test'
  root :to => "directory#index"
end
