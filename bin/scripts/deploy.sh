if [ $# -gt 0 ]; then
  git status
  read -n1 -rsp $'Press any key to continue or Ctrl+C to exit...\n'
  git add .
  git commit -m "$1"
  git push
  npm run build
  aws s3 sync build/ s3://marshallamey.com
else 
  echo 'Please include commit message!'
fi