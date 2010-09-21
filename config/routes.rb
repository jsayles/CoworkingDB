Directory::Application.routes.draw do
  resources :places
  resources :spaces

  root :to => "directory#index"
end
