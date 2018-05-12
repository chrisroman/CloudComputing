while true; do
  ping -c1 $RESERVATIONS_DB_HOST > /dev/null
  if [ $? -eq 0 ]; then
    break
  fi
done
echo "Successfully pinged the adress"
